USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_QueueConfiguration]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_QueueConfiguration](
	[QueueConfigurationId] [int] IDENTITY(1,1) NOT NULL,
	[AuctionId] [int] NOT NULL,
	[ItemsPerQueue] [int] NOT NULL,
	[Minutes] [int] NOT NULL,
	[FirstQueueClosingDate] [datetime] NOT NULL,
	[AllowWeekends] [bit] NOT NULL,
	[ClosingStartTime] [datetime] NOT NULL,
	[ClosingEndTime] [datetime] NOT NULL,
 CONSTRAINT [PK_vg_QueueConfiguration] PRIMARY KEY CLUSTERED 
(
	[QueueConfigurationId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
