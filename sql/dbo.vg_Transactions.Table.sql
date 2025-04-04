USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_Transactions]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_Transactions](
	[TransID] [int] IDENTITY(2000,1) NOT NULL,
	[InvoiceKey] [int] NOT NULL,
	[TransactionIndicator] [char](1) NOT NULL,
	[TransactionTry] [int] NOT NULL,
	[TransDate] [datetime] NOT NULL,
	[UserId] [uniqueidentifier] NOT NULL,
	[EngineResponse] [int] NOT NULL,
	[Amount] [decimal](18, 2) NOT NULL,
	[TenderID] [int] NOT NULL,
	[AccountType] [varchar](50) NOT NULL,
	[PaymentType] [char](2) NOT NULL,
	[ReferenceNumber] [varchar](50) NOT NULL,
	[TransactionType] [int] NOT NULL,
	[VGProductID] [int] NOT NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[vg_Transactions] ADD  CONSTRAINT [DF_vg_Transactions_TransactionTry]  DEFAULT ((1)) FOR [TransactionTry]
GO
